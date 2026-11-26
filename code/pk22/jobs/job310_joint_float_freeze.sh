#!/bin/bash
# job310 (pk22; the P0_LOG row 4851): freeze the joint_float producer for release_N (MR_JOINT's C-FLOAT control inputs), no compute.
# Evidence that the producer's bytes are those job157 ran: job157's console line 1 is astcheck_v1's 'AST OK <sha256> <path>' for the producer,
# which astcheck_v1 computes from the bytes it read (hashlib.sha256 of the file), printed by the same job script on the line before it ran the
# producer for N = 4 and 3; the current sha256 must equal it. Also: each output equals the text job157's console shows after its RUN line,
# and no listed file changed after the job (mtimes). The evidence goes to midrow/g4/mrx/JOINT_FLOAT_v1_FREEZE_EVIDENCE.txt; the manifest
# midrow/g4/mrx/MANIFEST_JOINT_FLOAT_v1.sha256 lists the producer, job157's script and console, the two outputs, astcheck_v1.py, the evidence
# file and this script; all become read-only.
set -u
set -o noclobber
S=/mnt/g2/release/root/code/pk22
X=$S/midrow/g4/mrx
P=$X/src/joint_float_v1.py
C=$S/jobs/job157_joint_float.console
J=$S/jobs/job157_joint_float.sh
A=$S/tools/astcheck_v1.py
O4=$X/out/joint_float_v1_n4.out
O3=$X/out/joint_float_v1_n3.out
E=$X/JOINT_FLOAT_v1_FREEZE_EVIDENCE.txt
M=$X/MANIFEST_JOINT_FLOAT_v1.sha256
[ -e $E ] && { echo "STOP: $E exists"; exit 3; }
[ -e $M ] && { echo "STOP: $M exists"; exit 3; }
for f in $P $C $J $A $O4 $O3; do [ -f $f ] || { echo "STOP: missing $f"; exit 3; }; done
NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
SP=$(/usr/bin/sha256sum $P | /usr/bin/cut -d' ' -f1)
SC=$(/usr/bin/awk 'NR==1 && $1=="AST" && $2=="OK"{print $3}' $C)
PC=$(/usr/bin/awk 'NR==1 && $1=="AST" && $2=="OK"{print $4}' $C)
[ -n "$SC" ] && [ "$SC" = "$SP" ] && [ "$PC" = "$P" ] || { echo "STOP: producer sha $SP vs job157 console '$SC' ($PC)"; exit 3; }
B4=$(/usr/bin/awk '/^RUN N=4 rc=0$/{f=1; next} /^RUN N=3 /{f=0} f' $C | /usr/bin/sha256sum | /usr/bin/cut -d' ' -f1)
B3=$(/usr/bin/awk '/^RUN N=3 rc=0$/{f=1; next} f' $C | /usr/bin/sha256sum | /usr/bin/cut -d' ' -f1)
H4=$(/usr/bin/sha256sum $O4 | /usr/bin/cut -d' ' -f1)
H3=$(/usr/bin/sha256sum $O3 | /usr/bin/cut -d' ' -f1)
[ "$B4" = "$H4" ] && [ "$B3" = "$H3" ] || { echo "STOP: console blocks vs outputs ($B4 $H4; $B3 $H3)"; exit 3; }
cat > $E <<EOF
JOINT_FLOAT_v1 freeze evidence (pk22, the P0_LOG row 4851), written by jobs/job310_joint_float_freeze.sh at $NOW.
1. The producer's bytes are those job157 ran: jobs/job157_joint_float.console line 1 is "AST OK $SC $PC", printed by
   tools/astcheck_v1.py, which prints the sha256 of the bytes it read (hashlib.sha256 of the file); job157's script ran that check and then
   the producer for N = 4 and 3. The producer's sha256 now: $SP (equal).
2. The two outputs are the text job157 printed: the console block after "RUN N=4 rc=0" has sha256 $B4, equal to joint_float_v1_n4.out's;
   the block after "RUN N=3 rc=0" has sha256 $B3, equal to joint_float_v1_n3.out's.
3. Modification times (stat): producer $(stat -c %y $P | /usr/bin/cut -c1-19), job157 script $(stat -c %y $J | /usr/bin/cut -c1-19), n4 output $(stat -c %y $O4 | /usr/bin/cut -c1-19), n3 output $(stat -c %y $O3 | /usr/bin/cut -c1-19),
   console $(stat -c %y $C | /usr/bin/cut -c1-19), astcheck_v1.py $(stat -c %y $A | /usr/bin/cut -c1-19): no listed file changed after job157's run.
4. Use: MR_JOINT's C-FLOAT control (mrj_cert_v1.py's JF pins) reads the two outputs; no bound uses them.
EOF
chmod a-w $P $C $A $E $S/jobs/job310_joint_float_freeze.sh
/usr/bin/sha256sum $P $J $C $O4 $O3 $A $E $S/jobs/job310_joint_float_freeze.sh > $M
chmod a-w $M
echo "MANIFEST $(/usr/bin/sha256sum $M | /usr/bin/cut -c1-16) entries $(/usr/bin/awk 'END{print NR}' $M)"
/usr/bin/sha256sum -c --quiet $M && echo "VERIFY OK"
/usr/bin/awk '{n=split($2, a, "/"); print "SHA8", substr($1, 1, 8), a[n]}' $M
echo "WRITABLE $(/usr/bin/awk '{print $2}' $M | while read p; do [ -w "$p" ] && echo w; done | /usr/bin/awk 'END{print NR}') of $(/usr/bin/awk 'END{print NR}' $M); manifest $(stat -c %A $M)"
echo "----"
/usr/bin/cat $E
