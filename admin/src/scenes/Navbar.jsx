import { useState, useEffect } from "react";
import { ProSidebar, Menu, MenuItem } from "react-pro-sidebar";
import { Box, IconButton, Typography } from "@mui/material";
import { Link } from "react-router-dom";
import 'react-pro-sidebar/dist/css/styles.css';
import { tokens } from "../theme";
import BarChartIcon from '@mui/icons-material/BarChart';
import FileUploadIcon from '@mui/icons-material/FileUpload';
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";

const Item = ({ title, to, icon, selected, setSelected }) => {
  const colors = tokens();
  return (
    <MenuItem
      active={selected === title}
      style={{
        color: colors.white,
      }}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const Navbar = ({ isCollapsed, setIsCollapsed }) => {
  const colors = tokens();
  
  // Initialize selected state from localStorage or default to "Dashboard"
  const [selected, setSelected] = useState(() => {
    const savedSelected = localStorage.getItem('selectedMenu');
    return savedSelected ? savedSelected : "Dashboard";
  });

  useEffect(() => {
    // Store the selected menu item in localStorage whenever it changes
    localStorage.setItem('selectedMenu', selected);
  }, [selected]);

  return (
    <Box
      sx={{
        height: "100vh",    
        position: "fixed",      
        top: 0,
        left: 0,
        zIndex: 1200,
        "& .pro-sidebar-inner": {
          background: `${colors.indigo[500]} !important`,
        },
        "& .pro-icon-wrapper": {
          backgroundColor: "transparent !important",
        },
        "& .pro-inner-item": {
          padding: "5px 35px 10px 20px !important",
        },
        "& .pro-inner-item:hover": {
          color: "#c2c6e1 !important",
        },
        "& .pro-menu-item.active": {
          color: "#9b9eb4 !important",
        },
      }}
    >
      <ProSidebar collapsed={isCollapsed}>
        <Menu iconShape="square">
          {/* LOGO AND MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            style={{
              margin: "10px 0 20px 0",
              color: colors.white,
            }}
          >
            {!isCollapsed && (
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                ml="15px"
              >
                <Typography variant="h3" color={colors.white}>
                  ODPRT Admin
                </Typography>
                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                  <MenuOutlinedIcon sx={{ color: colors.white }}/>
                </IconButton>
              </Box>
            )}
          </MenuItem>

          <Box paddingLeft={isCollapsed ? undefined : "10%"}>
            <Item
              title="Dashboard"
              to="/"
              icon={<BarChartIcon />}
              selected={selected}
              setSelected={setSelected}
            />
            <Item
              title="File Upload"
              to="/fileupload"
              icon={<FileUploadIcon />}
              selected={selected}
              setSelected={setSelected}
            />
          </Box>
        </Menu>
      </ProSidebar>
    </Box>
  );
};

export default Navbar;

