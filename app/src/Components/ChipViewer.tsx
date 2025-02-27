import PanZoom, {Element as PanZoomElement} from "@sasza/react-panzoom"
import { ReactElement, useContext } from "react"
import {payloadContext } from "../data/payload";
import { Link, LinkProps, useParams } from "react-router-dom";
export function ChipViewer() {

    // eslint-disable-next-line react-hooks/rules-of-hooks
    const payload = useContext(payloadContext);

    const elements: ReactElement<LinkProps>[] = [];
    {for (let col = 0; col < payload.codesX; col++){
        for (let row = 0; row < payload.codesY; row++) {
            elements.push(
            <PanZoomElement 
                id={`x=${col}y=${row}`} 
                x={col*(payload.codesX + payload.spacingX)}
                y={row * (payload.codesY + payload.spacingY)}
                family="root">
                <Link className="qrButton" to={`${col}+${row}`} style={{
                    "width": payload.codesX,
                    "height": payload.codesY
                }}>
                    {`${col},${row}`}
                </Link>
            </PanZoomElement>
            );
        }
    }}

    return <div id="chipViewer" style={{width: "100vw", height: "80vh"}}>
        <PanZoom>
            {elements}
        </PanZoom>
    </div>
}