import React from "react"

export type payload = {
    codesX: number,
    codesY: number,
    spacingX: number,
    spacingY: number,
    layer: Layer[]

}

export type Layer = {
    enabled: boolean,
    images: Image[]
}

export type Image = {
    url: string,
    anchor: [number, number],
    transforms: string,
}

export const payloadContext = React.createContext<payload>({
    codesX: 0,
    codesY: 0,
    spacingX: 0,
    spacingY: 0,
    layer: []
})