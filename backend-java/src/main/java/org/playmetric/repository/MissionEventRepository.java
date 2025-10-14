package org.playmetric.repository;

import org.playmetric.model.MissionEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface MissionEventRepository extends MongoRepository<MissionEvent, String> {}
