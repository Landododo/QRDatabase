import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import Navbar from "./Components/Navbar";
import project from "./data/project"

function App() {
  const [proj, setProj] = useState<project>()

  return (
    <>
      <Navbar projectName={"Test"} projectId="5" showAttributions={() => {}}/>
    </>
  )
}

export default App
