from deepeval import evaluate
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams, LLMTestCase
from deepeval.dataset import EvaluationDataset

from chatbot.backend.evaluation.params import QUERIES, GROUND_TRUTH
from chatbot.backend.inference.response_generator import ResponseGenerator
from chatbot.backend.services.vector_db.db import vector_db
from chatbot.backend.services.logger import logger


class Evaluator:
    def __init__(
        self,
    ):
        self.response_generator = ResponseGenerator()
        self.vector_db = vector_db
        self.logger = logger

    def _get_metrics(self):
        correctness_metric = GEval(
            name="Correctness",
            criteria="Determine whether the actual output is factually correct based on the expected output.",
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT,
            ],
            threshold=0.7,
        )

        contextual_precision_metric = GEval(
            name="Contextual Precision",
            criteria="Assess the precision of the actual output concerning the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
        )

        contextual_recall_metric = GEval(
            name="Contextual Recall",
            criteria="Determine how well the actual output recalls information from the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
        )

        faithfulness_metric = GEval(
            name="Faithfulness",
            criteria="Check the factual accuracy of the actual output based on the provided context.",
            evaluation_params=[
                LLMTestCaseParams.CONTEXT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
            ],
        )
        return {
            "correctness": correctness_metric,
            "contextual_precision": contextual_precision_metric,
            "contextual_recall": contextual_recall_metric,
            "faithfulness": faithfulness_metric,
        }

    def _get_test_cases(self):
        test_cases = []
        self.logger.info("[ResponseGenerator] generating responses")
        for query, ground_truth in zip(QUERIES, GROUND_TRUTH):
            _, context_list = self.vector_db.hybrid_search(query=query)
            response = self.response_generator._generate_answer(user_query=query)
            test_case = LLMTestCase(
                input=query,
                actual_output=response,
                expected_output=ground_truth,
                context=context_list,
            )
            test_cases.append(test_case)
        return test_cases

    def build_metrics_and_dataset(self):
        test_cases = self._get_test_cases()
        self.logger.info("[Evaluator] building the dataset")
        dataset = EvaluationDataset(test_cases=test_cases)
        metrics = self._get_metrics()
        return metrics, dataset

    def run_evaluation(self):
        metrics, dataset = self.build_metrics_and_dataset()
        self.logger.info("[Evaluator] evaluating the dataset")
        evaluate(dataset, [metric for metric in metrics.values()])


if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.run_evaluation()
