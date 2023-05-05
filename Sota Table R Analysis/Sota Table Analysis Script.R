##### Set dataset types#########################################################
# 1. Click "SOTA Table (dots).csv" and click "Import Dataset".
# 2. Set the "Delimiter" to "Semicolon".
# 3. Click "Import".
# Remember to "Set working directory" to the right folder. Then run these lines:

sota <- SOTA_Table_dots_
load("factor_levels.Rdata")
sota$Medium <- factor(sota$Medium, levels = medium_factor)
sota$Complexity <- factor(sota$Complexity, levels = complexity_factor)
sota$`Incentive Type` <- factor(sota$`Incentive Type`, levels = incentive_types_factor)
sota$`Time of payment` <- factor(sota$`Time of payment`, levels = time_of_payment_factor)
sota$Priorconcent <- factor(sota$Priorconcent, levels = prior_concent_factor)

# You dataset is now correctly formattet.