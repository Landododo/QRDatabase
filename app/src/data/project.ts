import React from "react"

export type project = {
    name?: "string",
    id?: "string",
}

export const ProjectContext = React.createContext<project>({})