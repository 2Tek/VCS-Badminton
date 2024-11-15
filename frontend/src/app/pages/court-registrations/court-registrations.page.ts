import { Component, OnInit } from '@angular/core';
import { CourtRegistrationService, Court, CourtRegistration } from '../../services/court-registration.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-court-registration',
  templateUrl: './court-registrations.page.html',
  styleUrls: ['./court-registrations.page.scss'],
})
export class CourtRegistrationsPage implements OnInit {
  courts: Court[] = [];
  registrationList: { [courtId: number]: CourtRegistration[] } = {};

  constructor(
    private authService: AuthService,
    private courtRegistrationService: CourtRegistrationService
  ) {}

  ngOnInit() {
    // Fetch courts and registration list
    this.fetchCourts();
    this.fetchRegistrations();
  }

  fetchCourts() {
    this.courtRegistrationService.getCourts();
    // Wait for courtsList to populate
    setTimeout(() => {
      this.courts = this.courtRegistrationService.courtsList;
      console.log('Courts:', this.courts); // Debug to ensure data
    }, 500); // Adjust timing as needed for async data
  }

  fetchRegistrations() {
    this.courtRegistrationService.getCourtRegistrations();
    // Wait for registrationList to populate
    setTimeout(() => {
      this.registrationList = this.courtRegistrationService.registrationList;
      console.log('Registrations:', this.registrationList); // Debug to ensure data
    }, 500); // Adjust timing as needed for async data
  }

  // Helper method to get registrations for a specific court
  getRegistrationsForCourt(courtId: number): CourtRegistration[] {
    return this.registrationList[courtId] || [];
  }
}
