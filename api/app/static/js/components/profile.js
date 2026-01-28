import { state } from '../state.js';
import { goalButtons } from '../main.js';

export function renderProfile() {
    if (!state.userProfile) return;
    document.getElementById('profile-name').textContent = state.userProfile.name;
    
    // Populate update-info form
    document.getElementById('update-name').value = state.userProfile.name;
    document.getElementById('update-age').value = state.userProfile.age;
    document.getElementById('update-height').value = state.userProfile.height_cm;
    document.getElementById('update-weight').value = state.userProfile.weight_kg;
    document.getElementById('update-sex').value = state.userProfile.sex;

    // Highlight current goal
    state.selectedGoal = state.userProfile.goal;
    goalButtons.forEach(b => {
         const isSelected = b.dataset.goal === state.selectedGoal;
         b.classList.toggle('bg-slate-900', isSelected);
         b.classList.toggle('text-white', isSelected);
         b.classList.toggle('bg-white', !isSelected);
         b.classList.toggle('border-slate-200', !isSelected);
    });
}
