<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\FileUploadController;
use App\Http\Controllers\PDFRegisterController;
use App\Http\Controllers\RelatedDocumentsController;


/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', [PDFRegisterController::class, 'index']);
//Route::get('/upload-file', [FileUploadController::class, 'createForm']);
Route::post('/upload-file', [FileUploadController::class, 'fileUpload'])->name('fileUpload');
Route::get('/related-document/{id}', [RelatedDocumentsController::class, 'getRelatedDocuments']);
Route::post('/related-document', [RelatedDocumentsController::class, 'removeRelatedDocument']);