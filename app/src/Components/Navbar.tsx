import {Box, IconButton} from "@mui/material";
import Divider from '@mui/material/Divider';
import Stack from '@mui/material/Stack';
import {Link} from "react-router";
import {Home, InfoRounded} from "@mui/icons-material";

export interface NavbarProps {
    projectName: string,
    projectId?: string,
    showAttributions: ()=>void,
}

const paths: Map<string, string> = new Map([
    ["Layout", ""],
    ["Code View", "/code"],
    ["Upload", "/upload"],
    ["Manage", "/manage"]
])


function Navbar(props: NavbarProps) {
    return (
        <Box component={"nav"} sx={{backgroundColor: 'palette.primary'}}>
            <Stack direction="row">
                <Stack spacing={2} direction="row" divider={<Divider orientation={"vertical"} flexItem/>}>
                    <IconButton component={Link} to={"/"} aria-label={"home"} color={"secondary"}>
                        <Home/>
                    </IconButton>
                    <h1>
                        {props.projectName ? `QR DB | ${props.projectName}` : "QR DB"}
                    </h1>
                </Stack>
                <Stack spacing={2} direction="row">
                    {[...paths.keys()].map((path, ix) => {
                        return (
                            <Link key={ix} to={props.projectId ? `/${props.projectId}${paths.get(path)}` : ""}
                                  className={props.projectId ? "" : "link-disabled"}>
                                {path}
                            </Link>
                            )
                    })}
                </Stack>
                <IconButton aria-label={"attributions"} onClick={props.showAttributions}>
                    <InfoRounded/>
                </IconButton>
            </Stack>
        </Box>
    )
}

export default Navbar