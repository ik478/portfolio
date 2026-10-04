import { Component, DestroyRef, effect, inject, input, signal } from '@angular/core';
import { HttpClient, httpResource } from '@angular/common/http';
import { Title } from '@angular/platform-browser';
import { Inactive } from '../inactive/inactive';

interface Stat { value: string; label: string }
interface Skill { name: string; level: number }
interface Project {
  id: number;
  title: string;
  description: string;
  tags: string[];
  gif: string | null;
  githubUrl: string | null;
}
interface Person {
  name: string;
  initials: string;
  role: string;
  tagline: string;
  about: string;
  email: string;
  stats: Stat[];
  skills: Skill[];
  projects: Project[];
}

@Component({
  selector: 'app-portfolio',
  imports: [Inactive],
  templateUrl: './portfolio.html',
  styleUrl: './portfolio.css',
})
export class Portfolio {
  private http = inject(HttpClient);
  private title = inject(Title);

  // The ":username" part of the link arrives here automatically
  username = input.required<string>();

  // Ask Python for THIS person's data
  person = httpResource<Person>(
    () => `/api/portfolio/${encodeURIComponent(this.username())}`
  );

  year = new Date().getFullYear();

  // Slider state
  index = signal(0);
  paused = signal(false);

  // Contact form state
  status = signal<'idle' | 'sending' | 'sent' | 'error'>('idle');

  constructor() {
    // Auto-slide every 4.5 seconds (pauses while the mouse is over the slider)
    const timer = setInterval(() => {
      const count = this.person.value()?.projects.length ?? 0;
      if (!this.paused() && count > 1) {
        this.index.update((i) => (i + 1) % count);
      }
    }, 4500);
    inject(DestroyRef).onDestroy(() => clearInterval(timer));

    // Browser tab title = person's name
    effect(() => {
      const p = this.person.value();
      if (p) this.title.setTitle(`${p.name} | Portfolio`);
    });
  }

  next(count: number) { this.index.update((i) => (i + 1) % count); }
  prev(count: number) { this.index.update((i) => (i - 1 + count) % count); }

  // Menu links: /kiran#about etc.
  link(id: string) { return `/${this.username()}#${id}`; }

  go(event: Event, id: string) {
    event.preventDefault();
    document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
  }

  send(nameBox: HTMLInputElement, emailBox: HTMLInputElement, msgBox: HTMLTextAreaElement) {
    if (!nameBox.value.trim() || !emailBox.value.trim() || !msgBox.value.trim()) return;

    this.status.set('sending');
    this.http
      .post(`/api/portfolio/${encodeURIComponent(this.username())}/contact`, {
        name: nameBox.value,
        email: emailBox.value,
        message: msgBox.value,
      })
      .subscribe({
        next: () => {
          this.status.set('sent');
          nameBox.value = '';
          emailBox.value = '';
          msgBox.value = '';
        },
        error: () => this.status.set('error'),
      });
  }
}