from versify.paths.v2_notes_note_id.get import ApiForget
from versify.paths.v2_notes_note_id.put import ApiForput
from versify.paths.v2_notes_note_id.delete import ApiFordelete


class V2NotesNoteId(
    ApiForget,
    ApiForput,
    ApiFordelete,
):
    pass
