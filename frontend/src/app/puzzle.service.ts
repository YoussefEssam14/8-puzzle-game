import { Injectable , inject } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import{
    RandomResponse , SolveRequest , SolveResponse , SolvableRequest , SolvableResponse , SampleResponse,
} from "./models";

const API = "http://localhost:8000/api";

@Injectable({
    providedIn : "root"
})

export class PuzzleService {
    private readonly http = inject(HttpClient);
    solvable(state : number[]){
        const body : SolvableRequest = {state};
        return this.http.post<SolvableResponse>(`${API}/solve/solvability` , body)
    }
    solve(req : SolveRequest){
        return this.http.post<SolveResponse>(`${API}/solve`,req);
    }
    compare(req : SolveRequest){
        return this.http.post<SolveResponse[]>(`${API}/solve/compare`,req);
    }
    random() {
        return this.http.get<RandomResponse>(`${API}/random?solvable=true`);
    }
    sample(){
        return this.http.get<SampleResponse>(`${API}/sample`);
    }
}