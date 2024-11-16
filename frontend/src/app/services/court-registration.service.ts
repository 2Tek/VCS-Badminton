import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Court {
  court_no: number;
  id: number;
  name: string;
  level: string;
  max_players: number;
  date: string;
  time: string;
}
export interface CourtRegistration {
  court_id: number;
  id: number;
  name: string;
  player_unique_id: string;
  reg_date_time: string;
  role: 'Player' | 'Waitlist';
  fee: string;
}

export interface CourtRegistrationsResponse {
  registrations: CourtRegistration[][];
  success: boolean;
}

export interface CourtRegistrationResponse {
  court_registration: CourtRegistration;
  success: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class CourtRegistrationService {
  url = environment.apiServerUrl;
  public courtsList: Court[] = [];
  public registrationList: { [courtId: number]: CourtRegistration[] } = {};

  constructor(private auth: AuthService, private http: HttpClient) {}

  getHeaders() {
    const headers = {
      headers: new HttpHeaders().set('Authorization', `Bearer ${this.auth.activeJWT()}`)
    };
    return headers;
  }

  getCourts() {
    //clear courtsList
    this.courtsList = [];
    // Fetch courts
    this.http.get<{ success: boolean; courts: Court[] }>(this.url + '/courts', this.getHeaders())
      .subscribe({
        next: (res) => {
          if (res.success) {
            for (const court of res.courts) {
              this.courtsList.push({
                court_no: court.court_no,
                id: court.id,
                name: court.name,
                level: court.level,
                max_players: court.max_players,
                date: court.date,
                time: court.time
              });
            }
          }
        },
        error: (err) => {
          console.error('Failed to fetch courts:', err);
        }
      });
  }

  getCourtRegistrations() {
    // clear registrationList
    this.registrationList = {};
    // Fetch court registrations
    this.http.get<CourtRegistrationsResponse>(`${this.url}/court-registrations`, this.getHeaders())
      .subscribe((res) => {
        if (res.success) {
          this.registrationsToList(res.registrations);
      }
    });
  }

  saveCourtRegistration(courtRegistration: Partial<CourtRegistration>) {
    return this.http.post<CourtRegistrationResponse>(`${this.url}/court-registrations`, courtRegistration, this.getHeaders());
  }

  // POST method to create a new court
  addCourt(courtData: Partial<Court>) {
    return this.http.post<{ success: boolean, court: Court }>(`${this.url}/courts`, courtData, this.getHeaders());
  }

  // DELETE method to remove a court
  removeCourt(courtId: number) {
    return this.http.delete<{ success: boolean }>(`${this.url}/courts/${courtId}`, this.getHeaders());
  }

  // PATCH method to update an existing court
  updateCourt(courtId: number, courtData: Partial<Court>) {
    return this.http.patch<{ success: boolean, court: Court }>(`${this.url}/courts/${courtId}`, courtData, this.getHeaders());
  }

  registrationsToList(registrations: CourtRegistration[][]) {
    registrations.forEach((court, index) => {
      if (court.length > 0) {
        const courtId = court[0].court_id;
        this.registrationList[courtId] = court;
      }
    });
  }

  //add function to add registration
  addRegistration(reg: Partial<CourtRegistration>) {
    return this.http.post<CourtRegistrationResponse>(`${this.url}/court-registrations`, reg, this.getHeaders());
  }

  //implement removeRegistration to api court-registration, sending paritial CourtRegistration
  removeRegistration(id: number) {
    return this.http.delete<CourtRegistrationResponse>(`${this.url}/court-registrations/${id}`,this.getHeaders());
  }
}
