import {BrainCircuit} from "lucide-react";

const Logo = () => {
    return(
        <div className="flex items-center gap-3">
            <BrainCircuit size={28} className="text-blue-500"/>

            <div>
                <h1 className="font-semibold text-lg">TraceMind</h1>
                <p className="text-xs text-zinc-500">AI Incident Investigator</p>
            </div>
        </div>
    );
};

export default Logo;