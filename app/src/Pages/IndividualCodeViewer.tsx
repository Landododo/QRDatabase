import { useParams } from "react-router-dom";

export function CodeViewer() {
    const {codeid} = useParams();
    return <><h1>{codeid}</h1></>
}