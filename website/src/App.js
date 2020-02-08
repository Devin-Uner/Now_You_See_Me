import React from "react"
import styled from "styled-components"

import Background from "./components/Background"
import Method from "./components/Method"
import Videos from "./components/Videos"

function App() {
  return (
    <>
      <HeaderWrapper>
        <Header>
          <div>
            <h1>Now You See Me</h1>
          </div>
          <div>
            <a>Pudding</a>
            <a>Methods</a>
            <a>Background</a>
          </div>
        </Header>
      </HeaderWrapper>
      <VideoWrapper>
        <Videos />
      </VideoWrapper>
      <Main>
        <BGWrapper>
          <Background />
        </BGWrapper>
        <MethodWrapper>
          <Method />
        </MethodWrapper>
      </Main>
    </>
  )
}

const HeaderWrapper = styled.div`
  background-color: #111;
  padding: 0.5rem;
`

const Header = styled.header`
  max-width: 1200px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
  margin: 0 auto;

  a {
    margin-left: 2rem;
    cursor: pointer;
  }
`

const Main = styled.main`
  max-width: 1200px;
  margin: 0 auto;
`

const VideoWrapper = styled.div`
  margin: 0 auto;
  max-width: 1700px;
  margin: 1rem auto;
`

const MethodWrapper = styled.div``

const BGWrapper = styled.div``

export default App
