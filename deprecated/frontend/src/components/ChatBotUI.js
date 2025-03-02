import { collection, addDoc } from "firebase/firestore";
import { db } from "../firebaseConfig";

import React, { useState, useEffect, useRef } from "react";
import {
  Box,
  Button,
  ScrollArea,
  Text,
  TextInput,
  Loader,
  Dialog,
  Group,
  FileButton,
  HoverCard,
  Rating,
  Modal,
} from "@mantine/core";
import { useDisclosure } from "@mantine/hooks";

import {
  IconSend,
  IconFileUpload,
  IconMessageChatbot,
} from "@tabler/icons-react";
import Markdown from "react-markdown";
import { fetchChatResponse, fetchEmailResponse } from "../utils/apiCalls";

const ChatbotUI = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isMailtoLoading, setIsMailtoLoading] = useState(false);
  const [isFeedbackLoading, setIsFeedbackLoading] = useState(false);
  const [file, setFile] = useState(null);
  const [commonQns, setCommonQns] = useState([
    // eslint-disable-line no-unused-vars
    "When is a Research Collaboration Agreement (RCA) required?",
    "My collaborator is asking for NUS (NDA/RCA/CRA/MOU) template. Where can I find them?",
    "What is IEP Contracting Hub?",
    "Where can I find the latest template for MOU, NDA, RCA, CRA and CTA?",
    "User account creation in the Pactly Contracting Hub?",
  ]); //use setCommonQns after retrieving common qns from backend
  const [recentQuery, setRecentQuery] = useState("");
  const [ratingOpened, { open: openRating, close: closeRating }] =
    useDisclosure(false); // state controlling feedback modal
  const [dialogOpened, { open, close }] = useDisclosure(false); // state controlling chatbot dialog
  const [rating, setRating] = useState(0); // stores user rating
  const [queryCount, setQueryCount] = useState(0); // count no. of queries per session
  const [feedbackText, setFeedbackText] = useState(""); // state for feedback text
  const [modalOpen, setModalOpen] = useState(false); // state for pop-up modal (for load chat history)
  const loadingButtonRef = useRef(null);
  const lastMessageRef = useRef(null);

  // this is the autoscroll feature
  useEffect(() => {
    if (loading && loadingButtonRef.current) {
      loadingButtonRef.current.scrollIntoView({
        // so that loading button can be seen after autoscroll
        behavior: "auto",
        block: "end",
      });
    }
  }, [loading]);

  // this is the autoscroll feature
  useEffect(() => {
    if (lastMessageRef.current) {
      lastMessageRef.current.scrollIntoView({
        behavior: "auto",
        block: "end",
        inline: "nearest",
      });
    }
  }, [messages]);

  // sending function
  const handleSend = async (query = "") => {
    const inputQuery =
      typeof query === "string" && query.trim() !== "" ? query : input;

    if (inputQuery.trim() !== "") {
      setMessages((prev) => [...prev, { text: inputQuery, sender: "user" }]);
      setRecentQuery(inputQuery);
      setInput("");
      setLoading(true);

      try {
        console.log(inputQuery);
        // send last 15 messages and query to backend
        const response = await fetchChatResponse(
          inputQuery,
          messages.slice(-15),
        );

        setMessages((prev) => {
          const updatedMessages = [...prev, { text: response, sender: "bot" }];
          // console.log to see what the history looks like
          console.log(
            "Sending history after bot response:",
            updatedMessages.slice(-15),
          );
          // set history into local storage
          localStorage.setItem(
            "history",
            JSON.stringify(updatedMessages.slice(-15)),
          );
          return updatedMessages;
        });
        streamBotResponse(response);
      } catch (error) {
        console.log("Error fetching chat response: ", error);
        setMessages((prev) => [
          ...prev,
          { text: "Sorry, I encountered an error.", sender: "bot" },
        ]);
      } finally {
        setLoading(false);
        // retrieve and parsing of local storage
        var retrievedObject = JSON.parse(localStorage.getItem("history"));
        console.log(retrievedObject);
      }
      setQueryCount((prevCount) => prevCount + 1);
    }
  };

  // this checks if there is history and ask user if they wish
  // to load old history
  const loadHistory = () => {
    const savedHistory = localStorage.getItem("history");
    if (savedHistory) {
      setModalOpen(true);
    }
  };

  const confirmLoadHistory = () => {
    const savedHistory = localStorage.getItem("history");
    if (savedHistory) {
      const history = JSON.parse(savedHistory);
      setMessages(history);
    }
    setModalOpen(false); // Close modal after confirming
    open(); // open up the chatbot
  };

  const cancelLoadHistory = () => {
    setModalOpen(false); // Close modal without loading history
    open(); //open up the chatbot
  };

  // upload chat history to firestore
  const saveMessages = async () => {
    try {
      await addDoc(collection(db, "chat history"), {
        messages: messages,
        timestamp: new Date(),
      });
      console.log("Chat session saved to Firestore.");
    } catch (error) {
      console.error("Error saving chat session to Firestore: ", error);
    }
  };

  // this closes the chatbot dialog and opens the feedback modal
  const handleClose = () => {
    close();
    openRating();
  };

  // Reset session-related states when the dialog or feedback closes
  const resetSession = () => {
    setMessages([]); // Clear all chat messages
    setInput(""); // Reset input field
    setRating(0); // Reset the rating
    setFile(null); // Reset uploaded file state
    setFeedbackText("");
    saveMessages();
  };

  // submit user rating and feedback function
  // linked w firestore db
  const handleSubmitRating = async () => {
    try {
      setIsFeedbackLoading(true);
      await addDoc(collection(db, "ratings"), {
        rating: rating, // User rating
        timestamp: new Date(), // Time of submission
        recentQuery: recentQuery, // The latest query the user submitted
        numberOfQueries: queryCount,
        feedback: feedbackText,
      });
      console.log("Rating submitted:", rating);
    } catch (e) {
      console.error("Error adding rating: ", e);
    } finally {
      setIsFeedbackLoading(false);
    }
    // Reset states and close dialogs
    closeRating();
    close();
    resetSession();
  };

  // When user closes the feedback modal without submitting
  const handleFeedbackModalClose = () => {
    closeRating();
    resetSession(); // Ensure session resets even if no rating is submitted
  };

  // placeholder file upload function
  const handleFileUpload = (file) => {
    setFile(file);
    setMessages((prev) => [
      ...prev,
      { text: `Uploaded file: ${file.name}`, sender: "user" }, // Show uploaded file name
    ]);
  };

  // Download .txt file of chat history before sending email to IEP
  const downloadChatHistory = () => {
    const chatHistory = messages
      .slice(-15)
      .map((msg, index) => `Message ${index + 1}: ${msg.text}`)
      .join("\n\n");

    const blob = new Blob([chatHistory], { type: "text/plain" });

    const link = document.createElement("a");
    link.href = URL.createObjectURL(blob);
    link.download = "Chat_History.txt";
    link.click();
  };

  // create auto generated email function
  const createMailtoLink = async () => {
    try {
      downloadChatHistory(); // download .txt chat history file

      // send last 15 messages and query to backend
      setIsMailtoLoading(true);
      const bodyText = await fetchEmailResponse(messages.slice(-15));
      const subject = encodeURIComponent("IEP Enquiry");
      const body = encodeURIComponent(bodyText);

      const mailtoLink = `mailto:iep-admin@nus.edu.sg?subject=${subject}&body=${body}`;
      window.location.href = mailtoLink;
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          text: "Sorry, I was unable to generate an email template.",
          sender: "bot",
        },
      ]);
      console.log("Error fetching email response: ", error);
    } finally {
      setIsMailtoLoading(false);
    }
  };

  // Stream the words at a fixed interval mimicking natural chatting
  const streamBotResponse = (response) => {
    const words = response.split(" ");
    let currentMessage = "";
    let index = 0;

    // Stream the words at a fixed interval
    const intervalId = setInterval(() => {
      if (index < words.length) {
        currentMessage += words[index] + " ";
        setMessages((prev) => {
          // Replace the latest bot message with the current streamed message
          const updatedMessages = [...prev];
          // If last message is bot, update it
          if (
            updatedMessages.length &&
            updatedMessages[updatedMessages.length - 1].sender === "bot"
          ) {
            updatedMessages[updatedMessages.length - 1].text = currentMessage;
          } else {
            // Otherwise, add a new bot message
            updatedMessages.push({ text: currentMessage, sender: "bot" });
          }
          return updatedMessages;
        });
        index++;
      } else {
        clearInterval(intervalId); // Stop when all words are displayed
      }
    }, 50); // Adjust delay for streaming speed (e.g., 150ms per word)
  };

  return (
    <>
      <Modal
        opened={modalOpen}
        onClose={() => setModalOpen(false)}
        title="Loading Chatbot History"
      >
        <Text>Would you like to load your previous chat history?</Text>

        <Group position="right" mt="md">
          <Button
            onClick={confirmLoadHistory}
            style={{ backgroundColor: "#003D7C", color: "#fff" }}
          >
            Yes, Load History
          </Button>
          <Button onClick={cancelLoadHistory} variant="outline" color="gray">
            Cancel
          </Button>
        </Group>
      </Modal>

      <Button
        onClick={() => {
          loadHistory();
        }} // Updated to check for history saved
        size="lg"
        style={{
          marginBottom: "20px",
          backgroundColor: "#003D7C",
          color: "#fff", // Text color
          "&:hover": {
            backgroundColor: "#002A5C", // Hover color
          },
          textAlign: "left",
          display: "block",
          position: "fixed",
          bottom: "5px",
          right: "20px",
        }}
      >
        Got a question to ask IEP? <br />
        Chat now!{" "}
        <IconMessageChatbot
          stroke={1.5}
          size={35}
          style={{
            marginLeft: "18px",
          }}
        />
      </Button>

      <Dialog
        opened={dialogOpened}
        withCloseButton
        onClose={handleClose} // Close the dialog
        size="xl" // Size of the dialog
        transitionProps={{
          transition: "fade",
          duration: 300,
        }}
        shadow="lg"
        padding="xl"
        style={{
          borderRadius: "10px",
          zIndex: 2000,
          position: "fixed",
          top: "50px",
          right: "10px", // Add a margin to the right side
          margin: "0",
          bottom: "0",
          maxWidth: "50vw", // Make the dialog responsive to screen width
          width: "100%", // Use 100% width up to the maxWidth
        }}
      >
        <Group align="flex-end">
          <Box
            p="lg"
            style={{
              width: "1000px",
              height: "650px",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <Text
              size="lg"
              weight={500}
              mb="md"
              style={{
                backgroundColor: "#003D7C",
                color: "#ffffff",
                padding: "10px",
                borderRadius: "5px",
              }}
            >
              <IconMessageChatbot
                size={30}
                stroke={1.5}
                style={{ marginRight: "10px", marginTop: "4px" }}
              />
              Chat with us - ODPRT IEP Chatbot
            </Text>

            <ScrollArea
              style={{ flex: 1, marginBottom: "10px" }}
              scrollbars="y"
              type="scroll"
            >
              <Box
                mb="md"
                style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}
              >
                {commonQns.map((question, index) => (
                  <Button
                    key={index}
                    onClick={() => handleSend(question)}
                    variant="light"
                    radius="lg"
                    color="#EF7C00"
                  >
                    {question}
                  </Button>
                ))}
              </Box>

              {recentQuery && (
                <Box
                  style={{
                    position: "sticky",
                    top: "-1px",
                    zIndex: 1000,
                    padding: "2px",
                    marginBottom: "20px",
                    backgroundColor: "white",
                  }}
                >
                  <HoverCard width={280} shadow="md">
                    <HoverCard.Target>
                      <Button
                        variant="light"
                        color="#003D7C"
                        onClick={createMailtoLink}
                        loading={isMailtoLoading}
                        style={{
                          display: "block",
                          marginBottom: "10px",
                          width: "325px",
                          boxShadow: "0px 1px 3px rgba(0, 0, 0, 0.1)",
                        }}
                      >
                        Need more help? Contact IEP-Admin email
                      </Button>
                    </HoverCard.Target>
                    <HoverCard.Dropdown>
                      <Text size="sm">
                        Please remember to attach downloaded Chat_History.txt
                        file to your email!
                      </Text>
                    </HoverCard.Dropdown>
                  </HoverCard>
                </Box>
              )}
              <Box
                style={{ display: "flex", flexDirection: "column", gap: "8px" }}
              >
                {messages.map((message, index) => (
                  <Box
                    key={index}
                    ref={index === messages.length - 1 ? lastMessageRef : null} // Set the ref on the last message
                    style={{
                      background:
                        message.sender === "user" ? "#f0f0f0" : "#e6f3ff",
                      paddingTop: "10px",
                      paddingBottom: "10px",
                      paddingRight: "17px",
                      paddingLeft: "17px",
                      marginBottom: "15px",
                      borderRadius: "20px", // bubble effect
                      display: "inline-block", // bubble fit to text
                      maxWidth: "60%",
                      alignSelf:
                        message.sender === "user" ? "flex-end" : "flex-start",
                      textAlign: message.sender === "user" ? "right" : "left",
                      boxShadow: "0px 1px 3px rgba(0, 0, 0, 0.1)", // add shadow to bubble
                      overflowWrap: "break-word",
                      wordBreak: "break-word",
                      flexShrink: 0,
                    }}
                  >
                    {message.sender !== "user" ? (
                      <Markdown>{message.text}</Markdown>
                    ) : (
                      <Text align="right">{message.text}</Text>
                    )}
                  </Box>
                ))}
                <div ref={lastMessageRef} />
              </Box>

              {loading && (
                <Box
                  ref={loadingButtonRef}
                  style={{
                    display: "flex",
                    justifyContent: "center",
                    padding: "10px",
                  }}
                >
                  <Loader color="orange" size="sm" />
                </Box>
              )}
            </ScrollArea>
            <Box style={{ display: "flex", height: "30px" }}>
              <TextInput
                placeholder="Type your message here..."
                value={input}
                onChange={(event) => setInput(event.currentTarget.value)}
                onKeyDown={(event) => {
                  if (event.key === "Enter") {
                    handleSend();
                  }
                }}
                style={{
                  flex: 1,
                  marginRight: "8px",
                  width: "300px",
                  border: "#003D7C",
                }}
              />

              <FileButton
                color="#EF7C00"
                onChange={handleFileUpload}
                accept="application/pdf,application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
              >
                {(props) => (
                  <HoverCard width={140} shadow="md">
                    <HoverCard.Target>
                      <Button {...props} style={{ marginRight: "8px" }}>
                        <IconFileUpload stroke={1.25} />
                      </Button>
                    </HoverCard.Target>
                    <HoverCard.Dropdown>
                      <Text size="xs">Upload Document</Text>
                    </HoverCard.Dropdown>
                  </HoverCard>
                )}
              </FileButton>

              <HoverCard width={100} shadow="md">
                <HoverCard.Target>
                  <Button
                    color="#EF7C00"
                    onClick={handleSend}
                    disabled={loading}
                  >
                    <IconSend stroke={1.25} />
                  </Button>
                </HoverCard.Target>
                <HoverCard.Dropdown>
                  <Text size="xs">Send Query</Text>
                </HoverCard.Dropdown>
              </HoverCard>
            </Box>
          </Box>
        </Group>
      </Dialog>
      {/* Modal component for user feedback - rating out of 5 stars*/}
      <Modal
        opened={ratingOpened}
        onClose={handleFeedbackModalClose}
        title="Thank you for using the ODPRT IEP chatbot. How well did our chatbot meet your expectations?"
        centered
      >
        <Box style={{ display: "flex", justifyContent: "center" }}>
          <Rating
            value={rating}
            onChange={setRating}
            size="xl"
            color="orange"
          />
        </Box>
        <TextInput
          value={feedbackText}
          onChange={(e) => setFeedbackText(e.target.value)}
          variant="filled"
          radius="md"
          label="Any additional feedback?"
          placeholder="Type your feedback here"
          style={{ marginTop: 10 }}
        />
        <Button
          fullWidth
          mt="md"
          onClick={handleSubmitRating}
          loading={isFeedbackLoading}
        >
          Submit Feedback
        </Button>
      </Modal>
    </>
  );
};

export default ChatbotUI;
