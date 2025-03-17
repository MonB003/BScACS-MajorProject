import React, { useEffect, useState } from 'react';
import { useNavigate } from "react-router-dom";
import FileCheckForm from '../FileForm/FileCheckForm'
import LogGenerator from '../Log/LogGenerator'
import UserFiles from './UserFiles';
import './Dashboard.css';
import Modal from "../Modal/Modal"

function Dashboard() {
  const navigate = useNavigate();
  const accessToken = sessionStorage.getItem('accessToken');
  const userID = sessionStorage.getItem('userID');
  const username = sessionStorage.getItem('username');

  const [openModal, setOpenModal] = useState(false);
  const [modalTitle, setModalTitle] = useState("");
  const [modalText, setModalText] = useState("");

  // Redirect to login if no token is present
  useEffect(() => {
    if (!accessToken || !userID) {
      navigate("/");
    }
  }, [accessToken, userID, navigate]);

  if (!accessToken || !userID) {
    return null; // Render nothing while redirecting
  }

  // Show modal and text
  const showModal = (title, text) => {
    setModalTitle(title);
    setModalText(text);
    setOpenModal(true);
  };

  return (
    <div id="toolkitPage">
      <div id="logoutDiv">
        <button onClick={() => {
          sessionStorage.clear(); // Clear data
          navigate("/")
        }}>Logout</button>
      </div>
      <h1 id="helloName">Dashboard for {username}</h1>
      <div id="dashboardContainer">
        <UserFiles userID={userID} username={username} showModal={showModal} />
        <FileCheckForm userID={userID} showModal={showModal} />
        <LogGenerator userID={userID} username={username} />
      </div>

      {openModal && <Modal closeModal={setOpenModal} titleText={modalTitle} bodyText={modalText} />}
    </div>
  )
}

export default Dashboard