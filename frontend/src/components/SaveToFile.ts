import fs from "fs";
import { ActionData } from "./ActionTypes";

export function SaveToFile(data: ActionData) {

    fs.writeFileSync(
        "src/data/action.json",

        JSON.stringify(data, null, 2)
    );
}