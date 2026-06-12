context = CandidateContext(
    key=self.settings.key,
    events=tuple(events),
    index=index,
    bar_number=bar_number,
    beat_in_bar=beat_in_bar,
    harmony_span=harmony_span,
    motif_target_step=motif_target_step,
    section_role=(
        section.role if section is not None else "free"
    ),
    section_transform=(
        section.transform if section is not None else "free"
    ),
)

candidate_steps = self._candidate_steps(..., context)
chosen_note, chosen_score = self._choose_candidate(candidate_steps, context)
