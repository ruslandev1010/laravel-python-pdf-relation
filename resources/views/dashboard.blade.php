@extends('layout.mainlayout')
@section('content')
<div class="container">
  <svg width="1140" height="800"></svg>
</div>

<div class="modal fade" id="linkModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="exampleModalLabel">Document Relation</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
        <form>
          <div class="form-group">
            <label for="current-document" class="col-form-label">Current Document</label>
            <input type="text" class="form-control" id="current-document">
          </div>
          <div class="form-group">
            <label for="related-document">Related Document</label>
            <select class="form-control" id="related-document">
            </select>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary" id="removeBtn">Remove</button>
      </div>
    </div>
  </div>
</div>

@endsection
