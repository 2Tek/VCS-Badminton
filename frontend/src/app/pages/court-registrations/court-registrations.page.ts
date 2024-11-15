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
  newCourt: Partial<Court> = {};
  canAddCourt = false;
  isSidebarOpen = false;
  newRegistration: { [courtId: number]: string } = {}; // Holds text box values per court

  constructor(
    private courtService: CourtRegistrationService,
    private authService: AuthService
  ) {}

  ngOnInit() {
    // Fetch courts and registration list
    this.fetchCourts();
    this.fetchRegistrations();
    this.checkPermissions();
  }

  fetchCourts() {
    this.courtService.getCourts();
    // Wait for courtsList to populate
    setTimeout(() => {
      this.courts = this.courtService.courtsList;
      console.log('Courts:', this.courts); // Debug to ensure data
    }, 500); // Adjust timing as needed for async data
  }

  fetchRegistrations() {
    this.courtService.getCourtRegistrations();
    // Wait for registrationList to populate
    setTimeout(() => {
      this.registrationList = this.courtService.registrationList;
      console.log('Registrations:', this.registrationList); // Debug to ensure data
    }, 500); // Adjust timing as needed for async data
  }

  // Helper method to get registrations for a specific court
  getRegistrationsForCourt(courtId: number): CourtRegistration[] {
    return this.registrationList[courtId] || [];
  }

  checkPermissions() {
    this.canAddCourt = this.authService.can('post:court'); // Check if the user has permission to add a court
  }

  toggleSidebar() {
    this.isSidebarOpen = !this.isSidebarOpen;
  }

  submitCourtForm() {
    if (this.newCourt.id && Number.isInteger(this.newCourt.id)) {
      // Update existing court (PATCH)
      this.courtService.updateCourt(this.newCourt.id, this.newCourt).subscribe(res => {
        if (res.success) {
          this.fetchCourts(); // Reload the courts after updating
        }
      });
    } else {
      // Add new court (POST)
      this.courtService.addCourt(this.newCourt).subscribe(res => {
        if (res.success) {
          this.fetchCourts(); // Reload the courts after adding
        }
      });
    }
  }

  //deleteCourt base on court id from form
  deleteCourt(courtId: number) {
    this.courtService.removeCourt(courtId).subscribe(res => {
      if (res.success) {
        this.fetchCourts(); // Reload the courts after deleting
      }
    });
  }

  saveRegistration(courtId: number): void {
    const playerUniqueId = this.authService.get_user_id(); // Retrieve player ID
    const reg = {
      court_id: courtId,
      name: this.newRegistration[courtId], // Get value for this court
      player_unique_id: playerUniqueId,
    };
  
    // Call service to POST registration
    this.courtService.addRegistration(reg).subscribe(
      (response) => {
        console.log('Registration saved successfully:', response);
        this.fetchRegistrations(); // Refresh the registrations list
        this.newRegistration[courtId] = ''; // Clear the input box for this court
      },
      (error) => {
        console.error('Error saving registration:', error);
      }
    );
  }
}
