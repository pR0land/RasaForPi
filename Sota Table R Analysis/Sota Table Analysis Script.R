##### SAVE FACTORS #############################################################

medium_factor <- levels(sota$Medium)
complexity_factor <- levels(sota$Complexity)
incentive_types_factor <- levels(sota$`Incentive Type`)
time_of_payment_factor <- levels(sota$`Time of payment`)
prior_concent_factor <- levels(sota$Priorconcent)
save(medium_factor, complexity_factor, incentive_types_factor, time_of_payment_factor, prior_concent_factor, file = "factor_levels.Rdata")


##### LOAD AND FORMAT DATASET###################################################

  # 1. Click "SOTA Table (dots).csv" and click "Import Dataset".
  # 2. Set the "Delimiter" to "Semicolon".
  # 3. Click "Import".
  # Remember to "Set working directory" to the right folder. Then run this:
  # ( Mark it all and press CTRL+ENTER )

sota2 <- SOTA_Table
load("factor_levels.Rdata")
sota2$Medium <- factor(sota2$Medium, levels = medium_factor)
sota2$Complexity <- factor(sota2$Complexity, levels = complexity_factor)
sota2$`Incentive Type` <- factor(sota2$`Incentive Type`, levels = incentive_types_factor)
sota2$`Time of payment` <- factor(sota2$`Time of payment`, levels = time_of_payment_factor)
sota2$Priorconcent <- factor(sota2$Priorconcent, levels = prior_concent_factor)

  # You dataset is now correctly formatted and called "sota".

################################################################################

sota <- SOTA_Table_dots_
  # Swap out "Pages" with specific column
empty <- which(is.na(sota$Pages))
sota <- sota[-empty, ]
