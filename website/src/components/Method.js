import React from "react"
import styled from "styled-components"
import logo from "../static/hackku_img.png"

const Method = () => {
  return (
    <>
      <FirstRow>
        <Uses>
          <h2>Use Cases</h2>
          <ul>
            <li>Security</li>
            <li>Privacy</li>
          </ul>
        </Uses>
        <ImgWrapper></ImgWrapper>
      </FirstRow>
      <h2>How We Did It</h2>
      <p>
        Maybe we should draw a thing around it. <br />
        Like a rectangle? <br />
        Yeah, that. <br /> Oh yeah, a rectangle around the box. <br />{" "}
        Yeeaaahhhhh, thats good.
      </p>
      <img src="" alt="The Base Idea" />
      <p></p>
      <img src="" alt="Some fine tuning" />
    </>
  )
}

const FirstRow = styled.div`
  display: flex;
  justify-content: space-between;
`

const ImgWrapper = styled.div`
  height: 400px;
  width: 500px;
  background: url(${logo});
  background-size: cover;
`

const Uses = styled.div`
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  img {
    max-width: 300px;
    width: auto;
  }
`

export default Method
