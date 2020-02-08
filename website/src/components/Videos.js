import React, { useRef } from "react"
import styled from "styled-components"
import YouTube from "react-youtube"

const Videos = () => {
  const onReady = event => {
    // access to player in all event handlers via event.target
    event.target.pauseVideo()
  }

  const opts = {
    height: "468",
    width: "768",
    playerVars: {
      autoplay: 1
    }
  }

  const vidOne = useRef(null)
  const vidTwo = useRef(null)

  const startVideos = () => {
    vidOne.current.internalPlayer.playVideo()
    vidTwo.current.internalPlayer.playVideo()
  }

  return (
    <>
      <Button onClick={startVideos}>Start the Videos</Button>
      <Wrapper>
        <YouTube
          ref={vidOne}
          videoId="Zj1muqpEDQI"
          opts={opts}
          onReady={onReady}
        />
        <YouTube
          ref={vidTwo}
          videoId="Zj1muqpEDQI"
          opts={opts}
          onReady={onReady}
        />
      </Wrapper>
    </>
  )
}

const Button = styled.button`
  display: block;
  font-size: 2rem;
  color: #ddd;
  background-color: #111;
  border: none;
  padding: 0.5rem;
  border: 2px solid #999;
  border-radius: 5px;
  margin: 0.5rem auto;
`

const Wrapper = styled.div`
  display: flex;
  justify-content: space-around;
`

export default Videos
