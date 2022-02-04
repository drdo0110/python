#전체
SELECT
	total.`number` AS `전체 조회 번호`,
	total.`count` AS `전체 조회 카운트`
FROM lotto_num_total AS total
ORDER BY total.`count` DESC;


#주간
#주 단위 변경시 python lotto_select.py에서 week 변경 후 실행
SELECT 
	weekRound.`number` AS `주간 조회 번호`,
	weekRound.`count` AS `주간 조회 카운트`
FROM lotto_num_week AS weekRound
ORDER BY COUNT DESC;

