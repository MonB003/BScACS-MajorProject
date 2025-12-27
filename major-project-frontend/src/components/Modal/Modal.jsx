import React from 'react'
import "./Modal.css"

function Modal({ closeModal, titleText, bodyText }) {
  return (
    <div className='modalDiv'>
      <div className='modalContainer'>
        <h1>{titleText}</h1>
        <p className='modalText'>{bodyText}</p>
        <button onClick={() => {
          closeModal(false)
        }}>Ok</button>
      </div>
    </div>
  )
}

export default Modal