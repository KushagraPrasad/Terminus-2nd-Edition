bool sf_w9(int tally_green, int pending_cnt, int journal_drift) {
  return tally_green != 0 && pending_cnt == 0;
}
