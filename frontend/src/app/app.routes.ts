import { Routes } from '@angular/router';
import { Portfolio } from './portfolio/portfolio';
import { Inactive } from './inactive/inactive';

export const routes: Routes = [
  { path: '', component: Inactive, pathMatch: 'full' },
  { path: ':username', component: Portfolio },
  { path: '**', component: Inactive },
];