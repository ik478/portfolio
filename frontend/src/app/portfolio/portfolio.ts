import {
  Component, DestroyRef, computed, effect, inject, input, signal, untracked,
} from '@angular/core';
import { HttpClient, httpResource, HttpErrorResponse } from '@angular/common/http';
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

  // SAFE accessor: never throws, even when the request failed.
  // Use data() in the template instead of person.value()
  data = computed<Person | undefined>(() =>
    this.person.hasValue() ? this.person.value() : undefined
  );

  // HTTP status of a failed request (or undefined)
  private errorStatus = computed<number | undefined>(() => {
    const err = this.person.error() as unknown;
    const res = err instanceof HttpErrorResponse
      ? err
      : (err as { cause?: unknown } | undefined)?.cause;
    return res instanceof HttpErrorResponse ? res.status : undefined;
  });

  // 404 -> show the inactive page in place
  notFound = computed(() => this.errorStatus() === 404);

  // Any other failure (500, network...) -> show an error message
  failed = computed(() => !!this.person.error() && this.errorStatus() !== 404);

  readonly year = new Date().getFullYear();

  // Slider state
  index = signal(0);
  paused = signal(false);

  // Contact form state
  status = signal<'idle' | 'sending' | 'sent' | 'error'>('idle');

  constructor() {
    // Browser tab title = person's name
    effect(() => {
      const p = this.data();
      if (p) this.title.setTitle(`${p.name} | Portfolio`);
    });

    // Reset UI state when the username changes
    effect(() => {
      this.username();
      untracked(() => {
        this.index.set(0);
        this.status.set('idle');
      });
    });

    // Auto-slide: only runs with 2+ projects and while not paused
    effect((onCleanup) => {
      const count = this.data()?.projects.length ?? 0;
      if (count < 2 || this.paused()) return;
      const t = setInterval(() => this.next(count), 4500);
      onCleanup(() => clearInterval(t));
    });

    inject(DestroyRef).onDestroy(() => this.title.setTitle('Portfolio'));
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
    if (this.status() === 'sending') return;
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