import { FormEvent, useContext, useState } from "react"
import { PayloadContext } from "../data/payload"
import { useNavigate } from "react-router";

export function CodeViewerLanding(props: {projectId: string, toastFunc: (msg: string) => void}){
    const payload = useContext(PayloadContext);
    const navigate = useNavigate();

    const onSubmit = (e: FormEvent) => {
        e.preventDefault();
        e.stopPropagation();
        const form = e.currentTarget as HTMLFormElement;;
        const x = Number((form.elements.namedItem("x") as HTMLInputElement)?.value);
        const y = Number((form.elements.namedItem("y") as HTMLInputElement)?.value);
        if (x < 0 || x >= payload.codesX || y < 0 || y >= payload.codesY) {
            props.toastFunc(`${x},${y} is out of bounds.`);
            return;
        }
        if(props.projectId === undefined) {
            props.toastFunc("Error: Project is undefined");
            navigate("/");
            return;
        }
        navigate(`../${x}+${y}`);
    } 

    return <form id="codeSelectForm" onSubmit={onSubmit}>
        <div>
            <label htmlFor="x">x coordinate:</label>
            <input type="number" name="x" id="codeSelectX" defaultValue={0} />
        </div>
        <div>
            <label htmlFor="x">y coordinate (cartesian):</label>
            <input type="number" name="y" id="codeSelectY" defaultValue={0}/>
        </div>
        <input type="submit" value="Jump to code" />
    </form>

    
}