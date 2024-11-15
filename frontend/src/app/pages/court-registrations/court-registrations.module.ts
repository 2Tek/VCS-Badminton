import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { CourtRegistrationsPage } from './court-registrations.page';

const routes: Routes = [
  {
    path: '',
    component: CourtRegistrationsPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  declarations: [CourtRegistrationsPage]
})
export class CourtRegistrationsPageModule {}
