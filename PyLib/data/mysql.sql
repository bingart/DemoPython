CREATE TABLE `node` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `title` varchar(64) NOT NULL,
    `finger` varchar(64) NOT NULL,
    `historyPath` varchar(1024) NOT NULL,	
    `createTime` datetime NOT NULL,
    `updateTime` datetime NOT NULL,
    `state` varchar(64) NOT NULL,		/* OK, ERROR */
    `errorCount` bigint(20) NOT NULL,
    `pathOrder` varchar(64) NOT NULL,	/* EXIT/ENTRY/MIDDLE */
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;

CREATE UNIQUE INDEX key_index ON node (finger);