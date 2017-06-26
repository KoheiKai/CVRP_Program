$latex = 'platex -interaction=nonstopmode -synctex=1';
$latex_silent = 'platex -interaction=batchmode';
$dvips = 'dvips';
$bibtex = 'pbibtex';
$makeindex = 'mendex -r -c -s jind.ist';
$aux_dir = 'output';
$out_dir = $aux_dir;
$dvi_previewer = 'start dviout'; # -pv option
$dvipdf = 'dvipdfmx -q %O -o %D %S';
if ($^O eq 'darwin') {
    $pvc_view_file_via_temporary = 0;
    $pdf_previewer = 'open -ga /Applications/Skim.app';
} else {
    $pdf_previewer = 'xdg-open';
}
$pdf_mode = 3;
$pdf_update_method = 0;
