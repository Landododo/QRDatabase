/* eslint-disable react-hooks/rules-of-hooks */
import PanZoom, { Element as PanZoomElement } from "@sasza/react-panzoom"
import { API as PanZoomAPI } from "@sasza/react-panzoom";
import { ReactElement, useContext, useEffect, useRef, useState } from "react"
import { payloadContext } from "../data/payload";
import { Link, LinkProps } from "react-router-dom";
import RestartAltIcon from '@mui/icons-material/RestartAlt';
import { IconButton } from "@mui/material";

export function ChipViewer() {
    const payload = useContext(payloadContext);
    const containerRef = useRef<HTMLDivElement>(null);
    const panZoomRef = useRef<PanZoomAPI>(null);

    const [codeSize, setCodeSize] = useState<number>(0);
    const [dimensionStart, setDimensionStart] = useState<[number, number]>([0, 0]);
    // Since our coordinate system is inverted, we need some other getY function
    const [clientHeight, setClientHeight] = useState<number>(0);
    const [resetVisible, setResetVisible] = useState<boolean>(false);

    // State to force refreshes on window resizing
    const [windowSizeTracker, updateSize] = useState<number>(1);

    // Calculate container aspect ratio on mount
    useEffect(() => {
        if (containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect();
            //const screenAspect = rect.width / rect.height;

            const codesSpacingNeedsX = payload.codesX + (payload.codesX-1) * payload.spacingX;
            const codesSpacingNeedsY = payload.codesX + (payload.codesX-1) * payload.spacingX;

            const ratioX = rect.width / codesSpacingNeedsX;
            const ratioY = rect.height / codesSpacingNeedsY;

            const codeSize = Math.min(ratioX, ratioY);
            // we had to constrain x, so y should start at on offset
            const offsets: [number, number] = [0,0];
            if(codeSize === ratioX){
                offsets[1] = (rect.height - codesSpacingNeedsY * codeSize)/2;
            } else {
                offsets[0] = (rect.width - codesSpacingNeedsX * codeSize)/2;
            }

            setCodeSize(codeSize);
            if (dimensionStart[0] != offsets[0] || dimensionStart[1] != offsets[1]){
                setDimensionStart(offsets);
            }
            
            if (clientHeight != rect.height) setClientHeight(rect.height);
            
            const handleResize = () => updateSize(prev => prev + 1);

            window.addEventListener("resize", handleResize);
            console.log("codeSize", codeSize);
            return () => window.removeEventListener("resize", handleResize);
        }
    }, [payload, clientHeight, dimensionStart, windowSizeTracker]);



    const elements: ReactElement<LinkProps>[] = [];
    if (clientHeight) {
        for (let col = 0; col < payload.codesX; col++) {
            for (let row = 0; row < payload.codesY; row++) {
                elements.push(
                    <PanZoomElement
                        key={`${col}-${row}`}
                        id={`x=${col}y=${row}`} 
                        // TODO: Find origin and set appropriate location for origin
                        x={dimensionStart[0] + col * (codeSize+ codeSize * payload.spacingX)}
                        y={dimensionStart[1] + clientHeight - (row * (codeSize + codeSize * payload.spacingY)) - codeSize}
                        family="root">
                        <Link className="qrButton" to={`${col}+${row}`} style={{
                            width: codeSize,
                            height: codeSize,
                            fontSize: 0.3*codeSize,
                            border: `${0.01 * codeSize}px solid black`
                        }}>
                            {`${col},${row}`}
                        </Link>
                    </PanZoomElement>
                );
            }
        }
    }

    return (
        <div id="chipViewer" ref={containerRef} style={{ width: "100vw", height: "95vh" }}>
            <PanZoom disabledMove zoomMin={0.8} zoomMax={10} onContainerZoomChange={({_, zoom}) => setResetVisible(zoom > 2)} ref={panZoomRef}>
                {elements}
            </PanZoom>
            <IconButton id="resetChipView" className={resetVisible ? "resetVisible" : ""} onClick={() => {
                if (panZoomRef.current) panZoomRef.current.reset();
            }}
                sx={{
                    backgroundColor: 'fuchsia',
                    '&:hover': {
                    backgroundColor: 'deeppink',
                    },
                    color: 'white',
                }}>
                <RestartAltIcon />
            </IconButton>
        </div>
    );
}