import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TutorialGroupsComponent } from './tutorial-groups.component';

describe('TutorialGroupsComponent', () => {
    let component: TutorialGroupsComponent;
    let fixture: ComponentFixture<TutorialGroupsComponent>;

    beforeEach(async () => {
        await TestBed.configureTestingModule({
            imports: [TutorialGroupsComponent],
        }).compileComponents();

        fixture = TestBed.createComponent(TutorialGroupsComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
