package org.playmetric.repository;

import org.playmetric.model.EconomyEvent;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface EconomyEventRepository extends MongoRepository<EconomyEvent, String> {}
