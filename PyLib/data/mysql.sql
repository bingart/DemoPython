CREATE TABLE `node` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `category` varchar(64) NOT NULL,	/* EXIT/ENTRY/MIDDLE/UNKNOWN */
    `title` varchar(64) NOT NULL,
    `finger` varchar(64) NOT NULL,
    `historyPath` varchar(1024) NOT NULL,
    `position` varchar(64) NULL,		/* NULL for ENTRY */
    `region` varchar(64) NULL,			/* NULL for ENTRY */
    `createTime` datetime NOT NULL,
    `updateTime` datetime NOT NULL,
    `state` varchar(64) NOT NULL,		/* CREATED, FETCHED, CLOSED */
    `errorCount` bigint(20) NOT NULL,
    `reserve` varchar(1024) NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;
CREATE UNIQUE INDEX key_index ON node (finger, category);

CREATE TABLE `path` (
    `id` bigint(20) NOT NULL AUTO_INCREMENT,
    `first` varchar(64) NOT NULL,
    `last` varchar(64) NOT NULL,
    `full` varchar(1024) NOT NULL,
    `createTime` datetime NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
AUTO_INCREMENT=1;

