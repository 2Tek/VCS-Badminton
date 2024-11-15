import { TestBed } from '@angular/core/testing';

import { CourtRegistrationService } from './court-registration.service';

describe('CourtRegistrationService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CourtRegistrationService = TestBed.get(CourtRegistrationService);
    expect(service).toBeTruthy();
  });
});
