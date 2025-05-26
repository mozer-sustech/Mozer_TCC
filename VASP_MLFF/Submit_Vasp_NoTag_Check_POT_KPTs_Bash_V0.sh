#!/bin/bash
# -------- By Wei Cao, May 2025, Bash version ----------



echo "===== Batch Job Start ====="
echo "1. Check IF POSCAR&POTCAR"
echo "2. Check KPOINTS"
echo "\n"
foldername="$PWD"

for dir in */; do
    INPUT="${dir%/}"
    cd "$foldername/$INPUT" || continue

    echo "========== Processing: $INPUT =========="

    # 元素提取与顺序比较
    potcar_elements=$(grep "VRHFIN" POTCAR | awk -F"[:=]" '{gsub(/^[ \t]+/, "", $2); print $2}' | tr '\n' ' ' | sed 's/ *$//')
    poscar_elements=$(sed -n '6p' POSCAR | tr -s ' ' ' ' | sed 's/^ *//;s/ *$//')

    if [[ "$potcar_elements" == "$poscar_elements" ]]; then
        echo "[OK]       $INPUT: POSCAR == POTCAR elements"

        if [ ! -e "submit_tag" ]; then
            cp "$foldername/script" .
            qsub -N "$INPUT" script
            sed -i 's/\r$//' INCAR POSCAR POTCAR KPOINTS
            echo "submit time at" > submit_tag
            date >> submit_tag
            echo "[SUBMITTED] $INPUT"
        else
            echo "[SKIPPED]  $INPUT: Already submitted"
        fi
    else
        echo "[MISMATCH] $INPUT: POSCAR ≠ POTCAR elements"
        echo "  POSCAR: $poscar_elements"
        echo "  POTCAR: $potcar_elements"
        echo "[WARNING]  $INPUT: Job not submitted due to element mismatch"
    fi

    # 显示 TITEL 行（赝势信息）
    grep "TITEL" POTCAR

    # 显示 KPOINTS 的第4行（带提示）
    kpt_line=$(sed -n '4p' KPOINTS)
    echo "[KPOINTS]  $INPUT mesh: $kpt_line"

    echo ""  # 空行美化输出
    cd "$foldername"
done

echo "===== Batch Job Done ====="
