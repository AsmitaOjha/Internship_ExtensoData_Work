Source: Chatgpt
That's a smart question, Asmita! ✅ Understanding **why we include or exclude columns** helps build **robust, trustworthy models**.

Here’s why we **chose the 20 features** you listed — and **why we excluded** the others.

---

### ✅ Features Included (and Why):

These are **useful, non-redundant, and relevant**:

| Feature                                                     | Reason for Inclusion                                                                           |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `transactionAmount`                                         | Obvious factor — large or unusual amounts may be fraudulent.                                   |
| `availableMoney`, `creditLimit`, `currentBalance`           | Financial capacity can reveal fraud patterns (e.g., fraudsters exhausting limits).             |
| `posEntryMode`, `posConditionCode`                          | Show how and where the transaction happened — e.g., chip vs swipe vs online.                   |
| `cardPresent`, `expirationDateKeyInMatch`, `cvv_mismatch`   | Indicate whether the card details were used correctly — crucial for detecting stolen card use. |
| `txn_hour`, `txn_day`, `txn_month`, `weekday`, `is_weekend` | Fraud often happens at odd hours, on weekends, or month ends.                                  |
| `account_age_days`, `age_bin`                               | New accounts are more likely to be targets of fraud.                                           |
| `acqCountry`, `merchantCountryCode`, `merchantCategoryCode` | Certain countries or merchant types may be riskier.                                            |
| `transactionType`                                           | Useful to differentiate between "purchase", "cash advance", etc.                               |

---

### ❌ Columns Excluded (and Why):

#### 1. **IDs / Identifiers (Too Specific, Not Generalizable):**

| Column            | Why We Dropped It                                                          |
| ----------------- | -------------------------------------------------------------------------- |
| `accountNumber`   | Unique for each person — model would **memorize**, not learn.              |
| `customerId`      | Same reason — **high cardinality**, no learning value.                     |
| `cardLast4Digits` | Too specific. Not useful unless patterns exist, which we can't generalize. |

---

#### 2. **Raw Dates (We Extracted Features Already):**

| Column                                                                                | Why We Dropped It                                                                       |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| `transactionDateTime`, `currentExpDate`, `accountOpenDate`, `dateOfLastAddressChange` | Already extracted **hour, day, month, age, weekday**. Keeping full datetime adds noise. |

---

#### 3. **Redundant / Duplicated Info:**

| Column                  | Why We Dropped It                                                                  |
| ----------------------- | ---------------------------------------------------------------------------------- |
| `cardCVV`, `enteredCVV` | Already captured logic with `cvv_mismatch`. Keeping raw values risks data leakage. |
| `weekday_name`          | Duplicate of `weekday` — text version, not needed for models.                      |

---

### 🧠 Summary:

| ✅ Included Features | Clear fraud signals, generalizable, and numeric-friendly.   |
| ------------------- | ----------------------------------------------------------- |
| ❌ Dropped Features  | IDs, raw dates, duplicates, or likely to cause overfitting. |

---

Would you like help running a **feature importance** check later (like using `RandomForestClassifier.feature_importances_`) to confirm which ones are most valuable?
