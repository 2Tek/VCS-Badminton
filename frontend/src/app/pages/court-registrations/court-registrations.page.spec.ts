import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CourtRegistrationsPage } from './court-registrations.page';

describe('CourtRegistrationsPage', () => {
  let component: CourtRegistrationsPage;
  let fixture: ComponentFixture<CourtRegistrationsPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CourtRegistrationsPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CourtRegistrationsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
