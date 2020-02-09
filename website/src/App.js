import React from "react"
import styled from "styled-components"
import YouTube from "react-youtube"
import Zoom from "react-reveal/Zoom"

import logo from "./static/hackku_img.png"
import willFace from "./static/willFace.jpg"
import evanFace from "./static/evanFace.jpg"
import devinFace from "./static/devinFace.jpg"
import maxFace from "./static/maxFace.jpg"

function App() {
  const onReady = event => {
    event.target.pauseVideo()
  }

  const opts = {
    height: "390",
    width: "640",
    playerVars: {
      autoplay: 1
    }
  }

  return (
    <>
      <Logo></Logo>
      <HeaderWrapper>
        <Header>
          <div>
            <h1>Now You See Me</h1>
            <div></div>
          </div>
        </Header>
      </HeaderWrapper>
      <VideoWrapper>
        {/* <video className="videoTag" autoPlay loop muted>
          <source src={sample} type="video/mp4" />
        </video> */}
      </VideoWrapper>
      <Main>
        <section>
          <h2>Our Goal</h2>
          <p>
            Revolutionizing safety and privacy, the people at{" "}
            <strong>Now You See Me </strong>
            have been working to keep our clients secure. Using facial
            recognition mixed with object detection, our product is able to
            remove clients from any camera feeds running Now You See Me. From
            hiding yourself from prying eyes to protecting the location of
            someone beloved, Now You See Me is your invisibility cloak in the
            digital world.
          </p>
        </section>
        <section>
          <h3>The Process</h3>
          <Zoom>
            <div>
              <div>
                <h5>Version 1</h5>
                <p>
                  The first version of our product was very basic. When
                  presented with a body to remove from the streamed video, it
                  would create a "ghost" outline of the body.
                </p>
              </div>
              <YouTube videoId="Zj1muqpEDQI" opts={opts} onReady={onReady} />
            </div>
            <div>
              <YouTube videoId="Zj1muqpEDQI" opts={opts} onReady={onReady} />
              <div>
                <h5>Version 2</h5>
                <p>
                  Our second iteration had the product creating a box around
                  bodies instead of a direct outline. This allowed for some
                  error margin when body parts moved, making a more fluid
                  visual.
                </p>
              </div>
            </div>
            <div>
              <div>
                <h5>Version 3</h5>
                <p>
                  The third stop in Now You See Me's journey is where the
                  product started to really show it's stuff. When in favorable
                  lighting, selected bodies all but disappeared when in frame.
                </p>
              </div>
              <YouTube videoId="Zj1muqpEDQI" opts={opts} onReady={onReady} />
            </div>
            <div>
              <YouTube videoId="Zj1muqpEDQI" opts={opts} onReady={onReady} />
              <div>
                <h5>Version 4</h5>
                <p>
                  The final version of Now You See Me includes some
                  optimizations on version 3, while having largely teh same
                  capabilities.
                </p>
              </div>
            </div>
          </Zoom>
        </section>
        <Team>
          <h3>Meet The Team</h3>
          <div>
            <div>
              <DevinFace></DevinFace>
              <h6>Devin Uner</h6>
            </div>
            <div>
              <EvanFace></EvanFace>
              <h6>Evan Mills</h6>
            </div>
            <div>
              <WillFace></WillFace>
              <h6>Will Smith</h6>
            </div>
            <div>
              <MaxFace></MaxFace>
              <h6>Max Farver</h6>
            </div>
          </div>
        </Team>
        <footer>
          <h5>Contact Us</h5>
          <p>
            Email: example@example.com <br />
            Phone: (555) 555-5555
          </p>
        </footer>
      </Main>
    </>
  )
}

const Logo = styled.div`
  position: fixed;
  top: 100px;
  right: 30px;
  height: 250px;
  width: 300px;
  background: url(${logo}) no-repeat;
  background-size: contain;
  z-index: 100;
`

const HeaderWrapper = styled.div`
  background-color: #111;
  padding: 0.5rem;
`

const Header = styled.header`
  max-width: 1100px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  margin: 0 auto;

  h1 {
    color: #990013;
  }
`

const Main = styled.main`
  max-width: 1100px;
  margin: 0 auto;

  section > div {
    display: flex;
    justify-content: space-between;
    margin: 1rem auto;

    > div {
      padding: 5px;
      display: flex;
      flex-direction: column;
      justify-content: center;
    }
  }

  h2 {
    font-size: 6rem;
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 3rem;
    margin-bottom: 0.75rem;
  }
  h4 {
    font-size: 2.5rem;
  }
  h5 {
    font-size: 1.75rem;
    color: #990013;
  }

  p {
    font-size: 1.5rem;
    line-height: 1.6;
    margin-bottom: 3rem;
    color: #aaa;

    strong {
      color: #ddd;
    }
  }

  footer {
    margin-top: 4rem;
    h5 {
      color: #ddd;
    }
  }
`

const Team = styled.section`
  margin-top: 4rem;
  > div > div {
    flex-direction: column;
    align-items: center;
    font-size: 2rem;
    > div {
      height: 200px;
      width: 200px;
      background-color: red;
      border-radius: 50%;
      margin-bottom: 1rem;
      border: 5px solid #990013;
    }
  }
`

const VideoWrapper = styled.div`
  margin: 0 auto;
  max-width: 1700px;
  height: 700px;
  max-height: 700px;
  margin: 1rem auto;
`
const DevinFace = styled.div`
  background: url(${devinFace});
  background-size: contain;
  background-position: center;
`
const EvanFace = styled.div`
  background: url(${evanFace});
  background-size: contain;
  background-position: center;
`
const WillFace = styled.div`
  background: url(${willFace});
  background-size: contain;
  background-position: center;
`
const MaxFace = styled.div`
  background: url(${maxFace});
  background-size: contain;
  background-position: center;
`

export default App
