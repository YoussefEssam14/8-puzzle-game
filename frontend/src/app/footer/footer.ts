import { Component } from '@angular/core';
import { MdbRippleModule } from 'mdb-angular-ui-kit/ripple';
import { MdbFormsModule } from 'mdb-angular-ui-kit/forms'
@Component({
  imports: [MdbRippleModule, MdbFormsModule],
  selector: 'app-footer',
  styleUrl: './footer.css',
  templateUrl: './footer.html',
})
export class Footer {
  readonly authorName: string = "Yousef Essam";
  readonly authorGithubLink: string = "https://github.com/YoussefEssam14";
  readonly authorLinkedinLink: string = "https://www.linkedin.com/in/youssef-essam-469ba5244/"
  readonly authorEmail: string = "youssefessameldinqw@gmail.com"
}
