import { useEffect, useState } from 'react'
import './App.css'
import Navbar from "./Components/Navbar";
import { project, ProjectContext } from "./data/project"
import { Outlet } from 'react-router-dom';

function App() {
  const [proj, setProj] = useState<project>({id: "5"})

  useEffect(() => {


    return () => {

    }
  })

  return (
    <>
      <Navbar projectName={"Test"} projectId="5" showAttributions={() => {}}/>
      <ProjectContext.Provider value={proj}>
        <Outlet/>
      </ProjectContext.Provider>
    </>
  )
}

export default App
