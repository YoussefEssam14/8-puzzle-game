import { Component, EventEmitter, input, output } from '@angular/core';
import { Input , Output } from '@angular/core';
@Component({
  selector: 'app-board',
  styleUrl: './board.css',
  templateUrl: './board.html',
})
export class Board {
  @Input() board : number[] = [];
  @Output() tileClick = new EventEmitter<number>();
  onClick(idx : number){
    this.tileClick.emit(idx);
  }

}