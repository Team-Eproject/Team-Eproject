console.log("register.js loaded");

const categorySelect =
    document.getElementById("category-select");

const foodSelect =
    document.getElementById("food-select");

const newCategoryInput =
    document.getElementById("new-category-input");

const newFoodInput = 
    document.getElementById("new-food-input");

// 初回カテゴリ取得
async function loadCategories() {

    const response = 
        await fetch("/api/foods/categories/");

    const categories =
        await response.json();

    console.log(categories);

    categories.forEach(category => {

        const option = 
            document.createElement("option");

        option.value = category.id;
        option.textContent = category.name;

        categorySelect.appendChild(option);
    });

    // 手動追加
    const newOption =
        document.createElement("option");

    newOption.value ="new";
    newOption.textContent = "+ カテゴリ追加";

    categorySelect.appendChild(newOption);
    
}

// カテゴリ変更
categorySelect.addEventListener(
    "change",
    async () => {

        const categoryID =
            categorySelect.value;

        // 未選択
        if (!categoryID || categoryID === "new") {

            foodSelect.innerHTML =
                '<option value="">食材選択</option>';

            return;
        }

        // 新カテゴリ入力表示
        if (categoryID === "new") {

            newCategoryInput.style.display =
                "block";

            foodSelect.innerHTML =
                '<option value="">食材選択</option>';

            return;
        }

        newCategoryInput.style.display =
            "none";
        
        // 食材取得
        const response =
            await fetch(
                `/api/foods/foods/?category=${categoryID}`
        );

        const foods =
            await response.json();

        // 初期化
        foodSelect.innerHTML =
            '<option value="">食材選択</option>';

        foods.forEach(food => {

            const option = 
                document.createElement("option");

            option.value = food.id;
            option.textContent = food.name;

            foodSelect.appendChild(option);
        });

        // 手動追加
        const newOption =
            document.createElement("option");

        newOption.value = "new";
        newOption.textContent = "+ 食材追加";

        foodSelect.appendChild(newOption);

    }
);

// 食材変更
foodSelect.addEventListener(
    "change",
    () => {

        if (foodSelect.value === "new") {

            newFoodInput.style.display =
                "block";
        } else {

            newFoodInput.style.display =
                "none";
        }
    }
);

// 初回実行
loadCategories();