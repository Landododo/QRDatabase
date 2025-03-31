/* eslint-disable react-hooks/rules-of-hooks */
import PanZoom, { Element as PanZoomElement } from "@sasza/react-panzoom"
import { ReactElement, useContext, useEffect, useRef, useState } from "react"
import { payloadContext } from "../data/payload";
import { Link, LinkProps } from "react-router-dom";

export function ChipViewer() {
    const payload = useContext(payloadContext);
    const containerRef = useRef<HTMLDivElement>(null);
    const [chipSize, setChipSize] = useState<number>(0);

    // Calculate container aspect ratio on mount
    useEffect(() => {
        if (containerRef.current) {
            const rect = containerRef.current.getBoundingClientRect();
            //const screenAspect = rect.width / rect.height;

            const codesSpacingNeedsX = payload.codesX + (payload.codesX-1) * payload.spacingX;
            const codesSpacingNeedsY = payload.codesX + (payload.codesX-1) * payload.spacingX;

            const ratioX = rect.width / codesSpacingNeedsX;
            const ratioY = rect.height / codesSpacingNeedsY;

            const chipSize = Math.min(ratioX, ratioY)

            setChipSize(chipSize);
            console.log("Computed chip size:", chipSize);
        }
    }, [payload]);

    const elements: ReactElement<LinkProps>[] = [];

    for (let col = 0; col < payload.codesX; col++) {
        for (let row = 0; row < payload.codesY; row++) {
            const effectiveRow = payload.codesY - row;
            elements.push(
                <PanZoomElement 
                    key={`${col}-${row}`}
                    id={`x=${col}y=${effectiveRow}`} 
                    // TODO: Find origin and set appropriate location for origin
                    x={col * (payload.codesX + payload.spacingX)}
                    y={effectiveRow * (payload.codesY + payload.spacingY)}
                    family="root">
                    <Link className="qrButton" to={`${col}+${effectiveRow}`} style={{
                        width: chipSize,
                        height: chipSize
                    }}>
                        {`${col},${row}`}
                    </Link>
                </PanZoomElement>
            );
        }
    }

    return (
        <div id="chipViewer" ref={containerRef} style={{ width: "100vw", height: "95vh" }}>
            <PanZoom disabledMove zoomMin={0.9}>
                {elements}
            </PanZoom>
        </div>
    );
}