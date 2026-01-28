import { state } from "../state.js";
import { goalButtons } from "../main.js";

export function renderProfile() {
    if (!state.userProfile) {
        console.warn("[Profile] Cannot render profile: missing userProfile.");
        return;
    }
    document.getElementById("profile-name").textContent = state.userProfile.name;
    
    const profileAge = document.getElementById("profile-age");
    const profileHeight = document.getElementById("profile-height");
    const profileWeight = document.getElementById("profile-weight");
    const profileSex = document.getElementById("profile-sex");
    const profileGoal = document.getElementById("profile-goal");
    const profileCalorieTarget = document.getElementById("profile-calorie-target");
    const profileProteinTarget = document.getElementById("profile-protein-target");

    if (profileAge) profileAge.textContent = state.userProfile.age;
    if (profileHeight) profileHeight.textContent = state.userProfile.height_cm;
    if (profileWeight) profileWeight.textContent = state.userProfile.weight_kg;
    if (profileSex) profileSex.textContent = state.userProfile.sex;
    if (profileGoal) profileGoal.textContent = state.userProfile.goal.replace("_", " ");
    if (profileCalorieTarget) profileCalorieTarget.textContent = Math.round(state.userProfile.calorie_target);
    if (profileProteinTarget) profileProteinTarget.textContent = Math.round(state.userProfile.protein_target);

    // Populate update-info form
    document.getElementById("update-name").value = state.userProfile.name;
    document.getElementById("update-age").value = state.userProfile.age;
    document.getElementById("update-height").value = state.userProfile.height_cm;
    document.getElementById("update-weight").value = state.userProfile.weight_kg;
    document.getElementById("update-sex").value = state.userProfile.sex;

    // Highlight current goal
    state.selectedGoal = state.userProfile.goal;
    goalButtons.forEach(b => {
         const isSelected = b.dataset.goal === state.selectedGoal;
         b.classList.toggle("bg-slate-900", isSelected);
         b.classList.toggle("text-white", isSelected);
         b.classList.toggle("bg-white", !isSelected);
         b.classList.toggle("border-slate-200", !isSelected);
    });
}
