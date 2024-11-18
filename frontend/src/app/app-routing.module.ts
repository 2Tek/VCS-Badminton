import { NgModule } from '@angular/core';
import { PreloadAllModules, RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  { path: '', loadChildren: './pages/tabs/tabs.module#TabsPageModule' },
  { path: 'court-registrations', loadChildren: './pages/court-registrations/court-registrations.module#CourtRegistrationsPageModule' },
  { path: '**', redirectTo: '', pathMatch: 'full' } // Fallback to avoid 404 errors
];
@NgModule({
  imports: [
    RouterModule.forRoot(routes, {
      preloadingStrategy: PreloadAllModules,
      useHash: false,
    })
  ],
  exports: [RouterModule]
})
export class AppRoutingModule {}
