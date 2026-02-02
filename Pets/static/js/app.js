
/**
 * Calculates the total household pet budget based on individual pet profiles.
 * @param {Array} petProfiles - An array of objects containing individual pet data.
 * @param {string} dietType - 'standard' or 'premium'
 */
function calculateHouseholdBudget(petProfiles, dietType) {
    // 1. CONSTANTS
    const NUTRITION_MATRIX = [
        [200, 250, 400],   // Row 0: Small
        [600, 800, 1200],  // Row 1: Medium
        [1200, 1500, 2500] // Row 2: Large
    ];

    const COST_FACTORS = {
        'standard': 0.002,
        'premium': 0.005
    };

    const TREAT_MULTIPLIER = 1.10;
    const DAYS_IN_MONTH = 30;

    let totalHouseholdMonthlyE = 0;
    let costFactor = COST_FACTORS[dietType];

    // 2. THE LOOP (Processing each pet in the array)
    petProfiles.forEach((pet, index) => {
        // Map 1-based UI input to 0-based array index
        let row = pet.size - 1;
        let col = pet.activity - 1;

        // Step A: Get base calories
        let baseC = NUTRITION_MATRIX[row][col];

        // Step B: final(C) = base(C) * 1.10 (if treats selected)
        let finalC = pet.includesTreats ? (baseC * TREAT_MULTIPLIER) : baseC;

        // Step C: Calculate this specific pet's monthly cost
        let petMonthlyCost = (finalC * costFactor) * DAYS_IN_MONTH;

        // Step D: Add to the running household total
        totalHouseholdMonthlyE += petMonthlyCost;

        console.log(`Pet #${index + 1} Daily Calories: ${finalC} kcal`);
    });

    return totalHouseholdMonthlyE.toFixed(2);
}

// --- EXAMPLE USAGE ---
const myPets = [
    { size: 1, activity: 2, includesTreats: true },  // Small, Normal, Treats
    { size: 3, activity: 1, includesTreats: false } // Large, Low, No Treats
];

const totalCost = calculateHouseholdBudget(myPets, 'standard');
console.log(`Total Monthly Budget: £${totalCost}`);