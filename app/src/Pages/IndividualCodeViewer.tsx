import { useContext } from "react";
import { Link, useParams } from "react-router-dom";
import Toast from "typescript-toastify";
import { PayloadContext } from "../data/payload";
import { ProjectContext } from "../data/project";
import { CodeViewerLanding } from "../Components/CodeViewerLanding";

export function CodeViewer() {
    const {codeid} = useParams();
    const project = useContext(ProjectContext);
    const payload = useContext(PayloadContext);

    const errorToast = (msg: string) => {
        new Toast({
            position: "top-right",
            toastMsg: msg,
            autoCloseTime: 5000,
            canClose: true,
            showProgress: true,
            pauseOnHover: true,
            pauseOnFocusLoss: true,
            type: "error",
            theme: "dark"
          });
    }
    let codeIdReadable = "";

    if (typeof codeid  === "string"){
        const [x, y] = codeid.split("+").map(Number)
        if (!(Number.isNaN(x) || y===undefined || x < 0 || x  >= payload.codesX || y < 0 || y >= payload.codesY)) {
            codeIdReadable = `code at ${x},${y}`
        } else {
            if(codeid !== "select") errorToast(`Invalid code: ${codeid}`);
        }
    }


    return <div id="codeViewer">
        <h1>{codeIdReadable ? `Viewing entries for ${codeIdReadable}` : "Select Code"}</h1>
        {!codeIdReadable ?
        //TODO: Fix ! operator
            <CodeViewerLanding projectId={project.id!} toastFunc={errorToast}/> 
        :
        <>
            <form style={{border: "2px solid var(--mui-palette-primary-main)", borderRadius: "10px", padding: "20px"}}>
                <div className="centered"> 
                    <h2>Manual File Upload</h2>
                    <p>
                        Files uploaded will be associated with this code. Use a (.zip) file to bulk upload files.<br />
                        <em>To scan an image file with multiple QR codes, use the project scope <Link to="../upload">upload</Link> page.</em>
                    </p>
                    
                    <label htmlFor="codeZip">Upload file(s): </label>
                    <input type="file" name="codeZip" id="codeZip" />
                </div><br/>
                <input type="submit" value="Upload" />
            </form>
            <br/>
            <p className="centered">(click on images to download)</p>
            <p className="centered"><Link to="../select">Return to code selector</Link></p>
            <p className="centered"><a href="#" className="centered">Download .zip</a></p>
            <div>
                <ul>
                    <li><span><a href="">Filename</a> (<a style={{color: "#eb4034"}}>Delete</a>)<br/>
                        <img src="/vite.svg" alt="test" />
                        </span>
                    </li>
                    <li><span><a href="">Filename</a> (<a style={{color: "#eb4034"}}>Delete</a>)<br/>
                        <img src="/vite.svg" alt="test" />
                        </span>
                    </li>
                    <li><span><a href="">Filename</a> (<a style={{color: "#eb4034"}}>Delete</a>)<br/>
                        <img src="/vite.svg" alt="test" />
                        </span>
                    </li>
                </ul>
            </div> 
        </>
        }
    </div>
}