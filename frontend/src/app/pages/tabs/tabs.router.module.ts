import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: 'tabs',
    component: TabsPage,
    children: [
      { path: 'user-page', loadChildren: '../user-page/user-page.module#UserPagePageModule' }, 
      { path: 'court-registrations', loadChildren: '../court-registrations/court-registrations.module#CourtRegistrationsPageModule' }, // Add this line
      {
        path: '',
        redirectTo: '/tabs/court-registrations',
        pathMatch: 'full'
      }
    ]
  },
  {
    path: '',
    redirectTo: '/tabs/court-registrations',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [
    RouterModule.forChild(routes)
  ],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}
